/**
 * Root layout — installs global providers and the authentication route guard.
 *
 * Provider order matters: gesture handler → safe-area → auth context wrap the
 * whole tree. `ProtectedRoutes` watches the auth state and redirects so that
 * logged-out users only ever see the (auth) group and logged-in users land in
 * (tabs). The splash screen is held until the icon fonts have registered.
 */
import { Stack, useRouter, useSegments } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { useIconFonts } from '@/src/hooks/use-icon-fonts';
import { AuthProvider, useAuth } from '@/src/contexts/AuthContext';

// Keep splash visible until icon fonts register.
SplashScreen.preventAutoHideAsync();

function ProtectedRoutes() {
  const { user, loading } = useAuth();
  const segments = useSegments() as string[];
  const router = useRouter();

  useEffect(() => {
    // Wait until the stored session has been restored before redirecting.
    if (loading) return;

    const inAuthGroup = segments[0] === '(auth)';
    const atRoot = segments.length === 0; // sitting on "/" with no group yet

    if (!user && !inAuthGroup) {
      // Logged out anywhere but the auth screens → send to login.
      router.replace('/(auth)/login');
    } else if (user && (inAuthGroup || atRoot)) {
      // Logged in but on an auth screen or the bare root → send into the app.
      router.replace('/(tabs)');
    }
  }, [user, loading, segments]);

  return (
    <Stack screenOptions={{ headerShown: false, animation: 'fade' }}>
      <Stack.Screen name="(auth)" />
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="lesson/[id]" options={{ presentation: 'card' }} />
      <Stack.Screen name="drill" options={{ presentation: 'card' }} />
      <Stack.Screen name="speak-practice" options={{ presentation: 'card' }} />
    </Stack>
  );
}

export default function RootLayout() {
  const [loaded, error] = useIconFonts();

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  if (!loaded && !error) return null;

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <AuthProvider>
          <StatusBar style="light" />
          <ProtectedRoutes />
        </AuthProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
