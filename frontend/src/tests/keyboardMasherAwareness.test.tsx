import { describe, expect, it } from 'vitest'
import { lotiContext } from '../features/loti/lotiContext'
import { scriptedBrain } from '../features/loti/scriptedBrain'

describe('Keyboard Masher Emotional Awareness', () => {
  const now = new Date('2026-10-28T15:00:00')

  it('changes Loti opening message when recentAnomaly is button_masher', () => {
    // 1. Normal context without anomaly -> opens with day or weakest
    const normalCtx = lotiContext({
      sessions: [],
      goals: { year: null, goals: {} },
      emotion: undefined,
      now,
      recentAnomaly: null,
    })
    const normalOpening = scriptedBrain.opening(normalCtx)
    expect(normalOpening?.id).not.toBe('mashing')

    // 2. Context with button masher anomaly -> opens with emotional awareness check-in
    const masherCtx = lotiContext({
      sessions: [],
      goals: { year: null, goals: {} },
      emotion: undefined,
      now,
      recentAnomaly: 'button_masher',
    })
    const masherOpening = scriptedBrain.opening(masherCtx)
    expect(masherOpening?.id).toBe('mashing')
    expect(masherOpening?.pose).toBe('think')
    expect(masherOpening?.text).toContain('super fast taps')
    expect(masherOpening?.text).toContain('rushed or distracted')

    // 3. User responds to the emotional awareness prompt
    // A. "Distracted"
    const respDistracted = scriptedBrain.respond('mashing', 'distracted', masherCtx)
    expect(respDistracted?.id).toBe('mashing-distracted')
    expect(respDistracted?.text).toContain('protected your score')

    // B. "Felt rushed"
    const respRushed = scriptedBrain.respond('mashing', 'rushed', masherCtx)
    expect(respRushed?.id).toBe('mashing-rushed')
    expect(respRushed?.text).toContain('No rush at all')

    // C. "Ready now"
    const respReady = scriptedBrain.respond('mashing', 'ready', masherCtx)
    expect(respReady?.id).toBe('mashing-ready')
    expect(respReady?.text).toContain('steady, and focused')
  })
})
