import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  pageExtensions:['ts','tsx'],
  eslint:{
    ignoreDuringBuilds:true
  }
};

export default nextConfig;
