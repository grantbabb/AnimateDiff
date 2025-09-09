import { useEffect, useMemo, useRef, useState } from 'react'

type TimeLapsePlayerProps = {
  frames: string[]
  frameIntervalMs?: number
  autoPlay?: boolean
  width?: number | string
  height?: number | string
}

export function TimeLapsePlayer({
  frames,
  frameIntervalMs = 500,
  autoPlay = false,
  width = '100%',
  height = 360,
}: TimeLapsePlayerProps) {
  const [isPlaying, setIsPlaying] = useState<boolean>(autoPlay)
  const [currentFrameIndex, setCurrentFrameIndex] = useState<number>(0)
  const intervalRef = useRef<number | null>(null)

  const totalFrames = frames.length
  const currentFrame = useMemo(() => frames[currentFrameIndex] ?? '', [frames, currentFrameIndex])

  useEffect(() => {
    if (!isPlaying || totalFrames === 0) {
      if (intervalRef.current) window.clearInterval(intervalRef.current)
      intervalRef.current = null
      return
    }

    intervalRef.current = window.setInterval(() => {
      setCurrentFrameIndex((prev) => (prev + 1) % totalFrames)
    }, frameIntervalMs)

    return () => {
      if (intervalRef.current) window.clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }, [isPlaying, totalFrames, frameIntervalMs])

  function handlePlayPauseToggle(): void {
    setIsPlaying((prev) => !prev)
  }

  function handleFrameChange(event: React.ChangeEvent<HTMLInputElement>): void {
    const nextIndex = Number(event.target.value)
    setCurrentFrameIndex(nextIndex)
  }

  if (totalFrames === 0) {
    return <div style={{ width, height, display: 'grid', placeItems: 'center', background: '#111', color: '#fff' }}>No frames</div>
  }

  return (
    <div style={{ width }}>
      <div style={{ position: 'relative', width: '100%', height }}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={currentFrame}
          alt={`Frame ${currentFrameIndex + 1} of ${totalFrames}`}
          style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 8, border: '1px solid #222' }}
        />
        <div
          style={{
            position: 'absolute',
            bottom: 8,
            left: 8,
            right: 8,
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            background: 'rgba(0,0,0,0.45)',
            padding: 8,
            borderRadius: 6,
            color: '#fff',
          }}
        >
          <button onClick={handlePlayPauseToggle} style={{ padding: '4px 10px', borderRadius: 4, border: '1px solid #444', background: '#1f1f1f', color: '#fff' }}>
            {isPlaying ? 'Pause' : 'Play'}
          </button>
          <input
            type="range"
            min={0}
            max={Math.max(0, totalFrames - 1)}
            step={1}
            value={currentFrameIndex}
            onChange={handleFrameChange}
            style={{ flex: 1 }}
          />
          <span style={{ fontVariantNumeric: 'tabular-nums' }}>
            {currentFrameIndex + 1}/{totalFrames}
          </span>
        </div>
      </div>
    </div>
  )
}

export default TimeLapsePlayer

