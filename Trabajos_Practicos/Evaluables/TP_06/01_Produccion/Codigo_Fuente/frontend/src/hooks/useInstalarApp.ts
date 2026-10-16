import { useEffect, useState } from 'react';

// Evento que dispara el navegador cuando la PWA se puede instalar.
interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

/** Permite mostrar un botón "Instalar app" cuando el navegador lo habilita. */
export function useInstalarApp() {
  const [evento, setEvento] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    const guardar = (e: Event) => {
      e.preventDefault();
      setEvento(e as BeforeInstallPromptEvent);
    };
    const instalada = () => setEvento(null);
    window.addEventListener('beforeinstallprompt', guardar);
    window.addEventListener('appinstalled', instalada);
    return () => {
      window.removeEventListener('beforeinstallprompt', guardar);
      window.removeEventListener('appinstalled', instalada);
    };
  }, []);

  const instalar = async () => {
    if (!evento) return;
    await evento.prompt();
    await evento.userChoice;
    setEvento(null);
  };

  return { puedeInstalar: evento !== null, instalar };
}
