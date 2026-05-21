# Original Repository Fix Notes

I reviewed the public GitHub repository and found these main issues:

1. The project is a monorepo with a FastAPI backend and an Expo / React Native mobile app. It is not designed as a normal one-click web app.
2. The README only explains backend + mobile startup, not a direct Chrome workflow.
3. The mobile package has `expo start --web`, but the dependency list is incomplete for reliable Expo Web usage. A web build normally needs `react-dom`, `react-native-web`, and Expo web runtime packages.
4. The mobile app imports `fetchApi` from `src/store/api`, but the shown API file in the repo is unfinished/empty. Store methods call `/incidents`, `/resources`, `/signals`, etc., so the frontend cannot correctly communicate with the backend until that client is implemented.
5. The mobile app is dependent on the backend being running at the right localhost URL. Without a configured API base URL and CORS-safe browser flow, Chrome will not show real data.
6. For quick judging/demo purposes, the easiest fix is a browser-only demo that simulates the pipeline locally and exposes all features in Chrome.

## Suggested real repo structure

Add this folder to the repo root:

```text
web-demo/
  index.html
```

Then update the README with:

```text
## Run in Chrome
Open web-demo/index.html in Chrome.
```

## Suggested Expo Web package additions if you want to keep React Native Web

Inside `mobile/package.json`, add/install:

```bash
npx expo install react-dom react-native-web @expo/metro-runtime
```

Also make sure React Native matches the Expo SDK version. For Expo SDK 50, use Expo-compatible versions through `npx expo install` instead of manually pinning mismatched versions.

## Suggested API client

The mobile app needs a real API client in `mobile/src/store/api.ts` or imports must be changed consistently. A minimal client should:

- define `BASE_URL`, for example `http://localhost:8000`
- set `Content-Type: application/json`
- parse JSON responses
- throw clean errors when backend is down

