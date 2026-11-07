import { getUserId, usingMocks } from '../assessment/tasks/taskSource'
import type { PillarId, PillarScore } from './pillars'
import { PILLAR_IDS } from './pillars'

export type ServerPillarData = {
  latest: number
  uncertainty: number
  average: number
  sessions: number
}

export type WhyThisDecision = {
  kind: 'harder' | 'easier' | 'style'
  reason: string
  at: string
}

export type CollaborationData = {
  status: 'ok' | 'not_enough_data' | 'unavailable'
  composite_score?: number
  dimension_scores?: Record<string, number | null>
  dimension_weights?: Record<string, number | null>
  growth_recommendation?: string
  evidence?: { typed_turns: number; marked_turns: Record<string, number> }
}

export type ProfileResponse = {
  user_id: string
  status: 'ok' | 'not_enough_data'
  sessions: number
  min_sessions: number
  pillars?: Partial<Record<PillarId, ServerPillarData | null>>
  archetype?: { name: string; confidence: number; model_id: string } | null
  archetype_reason?: string | null
  forecast?: { status: string; validated: boolean; mode: string; [key: string]: unknown } | null
  forecast_reason?: string | null
  collaboration?: CollaborationData | null
  why_this?: WhyThisDecision[]
}

export async function fetchProfile(
  userId = getUserId(),
  h = 1,
  fetchFn: (url: string) => Promise<Response> = fetch,
): Promise<ProfileResponse | null> {
  if (usingMocks()) return null
  try {
    const res = await fetchFn(`/v1/dashboard/profile?user_id=${encodeURIComponent(userId)}&h=${h}`)
    if (!res.ok) return null
    return (await res.json()) as ProfileResponse
  } catch {
    return null
  }
}

export async function fetchCollaborationScore(
  userId = getUserId(),
  fetchFn: (url: string) => Promise<Response> = fetch,
): Promise<CollaborationData | null> {
  if (usingMocks()) {
    return {
      status: 'ok',
      composite_score: 82.5,
      dimension_scores: {
        clarification: 85,
        critical_verification: 75,
        iteration: 90,
        autonomy: 80,
        responsible_use: 100,
      },
      dimension_weights: {
        clarification: 0.2,
        critical_verification: 0.25,
        iteration: 0.2,
        autonomy: 0.2,
        responsible_use: 0.15,
      },
      growth_recommendation: 'Challenge AI suggestions by asking counterexamples or edge cases.',
      evidence: { typed_turns: 12, marked_turns: { clarification: 4, critical_verification: 3, iteration: 3, autonomy: 2, responsible_use: 0 } },
    }
  }
  try {
    const res = await fetchFn(`/v1/coach/collaboration-score?user_id=${encodeURIComponent(userId)}`)
    if (!res.ok) return null
    return (await res.json()) as CollaborationData
  } catch {
    return null
  }
}

export function profileToPillars(profile: ProfileResponse): Record<PillarId, PillarScore> | null {
  if (profile.status !== 'ok' || !profile.pillars) return null
  const out = {} as Record<PillarId, PillarScore>
  for (const id of PILLAR_IDS) {
    const p = profile.pillars[id]
    if (p) {
      out[id] = { score: p.latest, uncertainty: p.uncertainty, coverage: 1, proxies: [] }
    } else {
      out[id] = { score: null, uncertainty: 50, coverage: 0, proxies: [] }
    }
  }
  return out
}
