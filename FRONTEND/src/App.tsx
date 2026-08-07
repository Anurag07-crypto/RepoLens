import { Route, Routes } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import LandingPage from '@/pages/LandingPage'
import ChatPage from '@/pages/ChatPage'
import SettingsPage from '@/pages/SettingsPage'
import NotFoundPage from '@/pages/NotFoundPage'
import { ThemeProvider } from '@/contexts/ThemeContext'

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(91,124,255,0.28),_transparent_40%),linear-gradient(135deg,_#040713_0%,_#090d21_100%)] text-slate-50">
        <AnimatePresence mode="wait">
          <Routes>
            <Route
              path="/"
              element={
                <motion.div key="landing" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.25 }}>
                  <LandingPage />
                </motion.div>
              }
            />
            <Route
              path="/chat"
              element={
                <motion.div key="chat" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.25 }}>
                  <ChatPage />
                </motion.div>
              }
            />
            <Route
              path="/settings"
              element={
                <motion.div key="settings" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -18 }} transition={{ duration: 0.25 }}>
                  <SettingsPage />
                </motion.div>
              }
            />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </AnimatePresence>
      </div>
    </ThemeProvider>
  )
}

export default App
