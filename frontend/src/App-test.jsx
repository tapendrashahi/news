function App() {
  return (
    <div style={{ padding: '40px', fontFamily: 'Arial', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
      <h1 style={{ color: '#1a73e8', fontSize: '48px' }}>✅ React is Working!</h1>
      <p style={{ fontSize: '24px' }}>If you see this, React has loaded successfully.</p>
      <p style={{ fontSize: '18px' }}>Current time: {new Date().toLocaleTimeString()}</p>
      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: 'white', borderRadius: '8px' }}>
        <h2>Testing Complete</h2>
        <p>React is rendering correctly. You can now restore the full app.</p>
      </div>
    </div>
  );
}

export default App;
