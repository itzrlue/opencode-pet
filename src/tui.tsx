/** @jsxImportSource @opentui/solid */
import { createSignal, onCleanup, For } from "solid-js"
import type { TuiPluginModule } from "@opencode-ai/plugin/tui"
import { FRAMES } from "./frames.js"

type Segment = { text: string; fg?: string | null; bg?: string | null }
type Size = "large" | "small"

function AnimatedPet(props: { size: Size; background: unknown; sessionId?: string }) {
  const [frameIndex, setFrameIndex] = createSignal(0)
  const frames = () => FRAMES[props.size]
  const working = () => props.size === "small" && Boolean(props.sessionId)
  const travel = props.size === "large" ? 10 : 0
  const offset = () => {
    if (working()) return 0
    const i = frameIndex()
    if (i < 6 || i >= 22) return Math.round(travel / 2)
    if (i < 14) return Math.round(((i - 6) / 7) * travel)
    return Math.round((1 - (i - 14) / 7) * travel)
  }
  const currentFrame = () => {
    const set = frames()
    const i = frameIndex()
    return working() ? set.work[i % set.work.length] : set.move[i % set.move.length]
  }
  const timer = setInterval(() => setFrameIndex((i) => (i + 1) % 28), 120)
  onCleanup(() => clearInterval(timer))

  return (
    <box flexDirection="column" alignItems="center" paddingTop={props.size === "large" ? 1 : 0}>
      <box flexDirection="column" paddingLeft={offset()} paddingRight={travel - offset()}>
        <For each={currentFrame() as Segment[][]}>
          {(row) => (
            <box flexDirection="row" height={1}>
              <For each={row}>
                {(segment) => (
                  <text fg={segment.fg ?? props.background} bg={segment.bg ?? props.background}>
                    {segment.text}
                  </text>
                )}
              </For>
            </box>
          )}
        </For>
      </box>
    </box>
  )
}

const plugin: TuiPluginModule & { id: string } = {
  id: "codex-pet",
  tui: async (api) => {
    const currentSessionId = () => {
      const route = api.route.current
      return route.name === "session" ? route.params.sessionID : undefined
    }
    api.slots.register({
      order: 55,
      slots: {
        home_logo: () => <AnimatedPet size="large" background={api.theme.current.background} />,
        sidebar_content: ({ session_id }) => (
          <AnimatedPet size="small" sessionId={session_id ?? currentSessionId()} background={api.theme.current.background} />
        ),
      },
    })
  },
}

export default plugin
