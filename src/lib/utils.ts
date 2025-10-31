// 辅助函数：处理基础路径
export function getBasePath(): string {
  return import.meta.env.BASE_URL || '/';
}

// 辅助函数：创建带有基础路径的链接
export function createUrl(path: string): string {
  const basePath = getBasePath();
  // 确保路径以 / 开头
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  // 确保基础路径以 / 开头且不以 / 结尾（除了根路径）
  const cleanBase = basePath.endsWith('/') && basePath !== '/'
    ? basePath.slice(0, -1)
    : basePath;
  return `${cleanBase}${cleanPath}`;
}