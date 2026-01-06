import '../../styles/globals.css';
import type { AppProps } from 'next/app';
import { AuthProvider } from '../contexts/auth';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}