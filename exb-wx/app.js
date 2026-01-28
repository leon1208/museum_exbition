// app.js
import { api } from './utils/api.js'

App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 执行登录流程
    this.performLogin()

    // 设置 InnerAudioContext 的播放选项
    wx.setInnerAudioOption({
      obeyMuteSwitch: false // 设置为 false，即使在静音模式下也能播放声音
    });
  },
  
  // 执行登录流程
  performLogin() {
    wx.login({
      success: res => {
        if (res.code) {
          // 发送 res.code 到后台换取 access_token
          api.login(res.code)
            .then(response => {
              if (response.code === 200) {
                // 登录成功，保存 access_token
                wx.setStorageSync('access_token', response.data.access_token);
                
                // 可以选择性地保存其他用户信息
                if (response.data.user_info) {
                  wx.setStorageSync('user_info', response.data.user_info);
                }
                
                console.log('登录成功', response);
                
                // 更新登录状态
                this.globalData.isLoginCompleted = true;
                
                // 通知其他页面登录已完成
                if (this.onLoginSuccess) {
                  this.onLoginSuccess(response.data);
                }
                
                // 通知所有等待登录完成的页面
                if (this.loginCallbacks && this.loginCallbacks.length > 0) {
                  this.loginCallbacks.forEach(callback => callback(response.data));
                  this.loginCallbacks = [];
                }
              } else {
                console.error('登录失败', response);
                // 即使登录失败也标记为完成，因为有些接口可能不需要登录
                this.globalData.isLoginCompleted = true;
              }
            })
            .catch(error => {
              console.error('登录请求失败', error);
              // 即使登录失败也标记为完成，因为有些接口可能不需要登录
              this.globalData.isLoginCompleted = true;
            });
        } else {
          console.error('获取用户登录态失败', res.errMsg);
          // 即使登录失败也标记为完成，因为有些接口可能不需要登录
          this.globalData.isLoginCompleted = true;
        }
      },
      fail: err => {
        console.error('调用wx.login失败', err);
        // 即使登录失败也标记为完成，因为有些接口可能不需要登录
        this.globalData.isLoginCompleted = true;
      }
    });
  },
  
  globalData: {
    userInfo: null,
    isLoginCompleted: false, // 添加登录状态标识
    loginCallbacks: [] // 存储等待登录完成的回调函数
  },
  
  // 等待登录完成的方法
  waitForLogin: function(callback) {
    if (this.globalData.isLoginCompleted) {
      // 如果已经登录完成，直接执行回调
      callback && callback();
    } else {
      // 否则将回调加入队列，等待登录完成时执行
      this.loginCallbacks = this.loginCallbacks || [];
      this.loginCallbacks.push(callback);
    }
  }
})