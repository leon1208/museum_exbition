// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })

    // 设置 InnerAudioContext 的播放选项
    wx.setInnerAudioOption({
      obeyMuteSwitch: false // 设置为 false，即使在静音模式下也能播放声音
    });
  },
  globalData: {
    userInfo: null
  }
})
