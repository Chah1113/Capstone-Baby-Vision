/**
 * 화면 좌표 ↔ 영상 실제 좌표 변환(정규화) 유틸리티
 *
 * - 프론트 캔버스 위에서 사용자가 찍은 좌표를 0.0~1.0 범위로 정규화
 * - 서버에서 받은 정규화 좌표를 현재 화면 크기에 맞게 역변환
 */

/**
 * 화면 픽셀 좌표 → 정규화 좌표 (0.0~1.0)
 * @param {number} px - 화면 x 픽셀
 * @param {number} py - 화면 y 픽셀
 * @param {number} screenWidth - 화면 너비
 * @param {number} screenHeight - 화면 높이
 * @returns {number[]} [normalizedX, normalizedY]
 */
export function pixelToNormalized(px, py, screenWidth, screenHeight) {
  return [px / screenWidth, py / screenHeight];
}

/**
 * 정규화 좌표 → 화면 픽셀 좌표
 * @param {number} nx - 정규화 x (0.0~1.0)
 * @param {number} ny - 정규화 y (0.0~1.0)
 * @param {number} screenWidth - 화면 너비
 * @param {number} screenHeight - 화면 높이
 * @returns {number[]} [pixelX, pixelY]
 */
export function normalizedToPixel(nx, ny, screenWidth, screenHeight) {
  return [Math.round(nx * screenWidth), Math.round(ny * screenHeight)];
}

/**
 * 정규화 좌표 배열을 화면 좌표 배열로 변환
 * @param {number[][]} normalizedPoints - [[nx, ny], ...]
 * @param {number} screenWidth
 * @param {number} screenHeight
 * @returns {number[][]} [[px, py], ...]
 */
export function normalizedPointsToPixels(
  normalizedPoints,
  screenWidth,
  screenHeight
) {
  return normalizedPoints.map(([nx, ny]) =>
    normalizedToPixel(nx, ny, screenWidth, screenHeight)
  );
}
