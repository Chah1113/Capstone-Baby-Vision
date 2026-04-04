/**
 * 메인 서버 통신용 API 클라이언트
 * - docs/api_specs.md 기준으로 구현
 */

// TODO: 실제 서버 주소로 변경
const BASE_URL = "http://localhost:8000/api";

/**
 * 위험 구역 목록을 서버에서 가져온다.
 */
export async function fetchZones() {
  const response = await fetch(`${BASE_URL}/zones`);
  const data = await response.json();
  return data.zones;
}

/**
 * 새 위험 구역을 서버에 저장한다.
 * @param {string} name - 구역 이름
 * @param {number[][]} points - 정규화 좌표 배열 [[x, y], ...]
 */
export async function createZone(name, points) {
  const response = await fetch(`${BASE_URL}/zones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, points }),
  });
  return response.json();
}

/**
 * 위험 구역을 삭제한다.
 * @param {string} zoneId - 삭제할 구역 ID
 */
export async function deleteZone(zoneId) {
  const response = await fetch(`${BASE_URL}/zones/${zoneId}`, {
    method: "DELETE",
  });
  return response.json();
}

/**
 * 알림 내역을 조회한다.
 * @param {number} limit - 가져올 개수
 * @param {number} offset - 시작 위치
 */
export async function fetchAlerts(limit = 20, offset = 0) {
  const response = await fetch(
    `${BASE_URL}/alerts?limit=${limit}&offset=${offset}`
  );
  return response.json();
}

/**
 * FCM 토큰을 서버에 등록한다.
 * @param {string} fcmToken - Firebase Cloud Messaging 토큰
 */
export async function registerFcmToken(fcmToken) {
  const response = await fetch(`${BASE_URL}/users/fcm-token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fcm_token: fcmToken }),
  });
  return response.json();
}

/**
 * 실시간 영상 스트림 URL을 가져온다.
 */
export async function getStreamUrl() {
  const response = await fetch(`${BASE_URL}/stream/url`);
  const data = await response.json();
  return data.stream_url;
}
