import './App.css'
import TimeLapsePlayer from './components/TimeLapsePlayer'

function App() {
  const demoFrames = [
    'https://dummyimage.com/800x360/1f2937/ffffff&text=Weather+Frame+1',
    'https://dummyimage.com/800x360/111827/ffffff&text=Weather+Frame+2',
    'https://dummyimage.com/800x360/374151/ffffff&text=Weather+Frame+3',
    'https://dummyimage.com/800x360/4b5563/ffffff&text=Weather+Frame+4',
    'https://dummyimage.com/800x360/6b7280/ffffff&text=Weather+Frame+5',
  ]

  return (
    <div style={{ padding: 24 }}>
      <h1>Extreme Event Dashboard</h1>
      <p style={{ color: '#555', marginBottom: 16 }}>
        Time-lapse preview of weather patterns (demo frames).
      </p>
      <TimeLapsePlayer frames={demoFrames} frameIntervalMs={600} autoPlay={false} />
    </div>
  )
}

export default App
