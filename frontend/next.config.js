/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',
  
  // React strict mode (enabled by default in Next.js 15)
  reactStrictMode: true,
  
  // TypeScript configuration
  typescript: {
    // Don't fail build on type errors during development
    ignoreBuildErrors: false,
  },
  
  // ESLint configuration
  eslint: {
    // Don't fail build on ESLint errors during development
    ignoreDuringBuilds: false,
  },
  
  // Image optimization (disabled for Docker builds)
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;

