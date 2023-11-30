const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    proxy: {
      "/api": {
        target: "http://0.0.0.0:5000",
        changeOrigin: true,
        ws: true, // 为了使 websocket 也能使用代理
      },
      "/socket.io": {
        target: "http://0.0.0.0:5000",
        changeOrigin: true,
        ws: true,
      },
    },
  },
});
