// pages/my/index.js
Page({
  data: {
    defaultAvatarUrl: 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0',
    userInfo: {},
    version: '1.0.0',
    currentTab: 2 // 默认选中"我的"页面
  },

  onLoad() {
    this.loadUserInfo();
    this.getVersion();
    // 设置当前页面为"我的"页面
    this.setData({
      currentTab: 2
    });
  },

  loadUserInfo() {
    // 从全局数据或本地存储获取用户信息
    const app = getApp();
    const userInfo = wx.getStorageSync('userInfo') || {};
    this.setData({
      userInfo: userInfo
    });
  },

  getVersion() {
    // 获取小程序版本号
    const version = wx.getAccountInfoSync().miniProgram.version || '1.0.0';
    this.setData({
      version: version
    });
  },

  // 使用新的方式获取头像和昵称
  onChooseAvatar(e) {
    const { avatarUrl } = e.detail;
    const userInfo = this.data.userInfo;
    userInfo.avatarUrl = avatarUrl;
    
    // 自动获取用户昵称（如果可以的话）
    this.setData({
      userInfo: userInfo
    });
    
    // 保存到本地缓存
    wx.setStorageSync('userInfo', userInfo);
  },

  onInputChange(e) {
    const nickName = e.detail.value
    const userInfo = this.data.userInfo;
    userInfo.nickName = nickName;

    this.setData({
      userInfo: userInfo
    })
    // 保存到本地缓存
    wx.setStorageSync('userInfo', userInfo);
  },

  // 获取用户手机号
  getPhoneNumber(e) {
    if (e.detail.errMsg === 'getPhoneNumber:ok') {
      // 这里需要调用后端接口解密手机号
      const encryptedData = e.detail.encryptedData;
      const iv = e.detail.iv;
      
      // 示例：调用后端接口获取手机号
      // this.getDecryptedPhone(encryptedData, iv);
      
      console.log('获取手机号成功', e.detail);
      wx.showToast({
        title: '手机号获取成功',
        icon: 'success'
      });
    } else {
      console.log('获取手机号失败', e.detail.errMsg);
      wx.showToast({
        title: '手机号获取失败',
        icon: 'none'
      });
    }
  },

  // 示例：调用后端接口解密手机号
  getDecryptedPhone(encryptedData, iv) {
    // 这里应该调用你的后端接口来解密手机号
    // 示例代码：
    /*
    const code = this.getLoginCode(); // 需要先获取登录凭证
    wx.request({
      url: 'your_backend_api/decryptPhone',
      method: 'POST',
      data: {
        encryptedData,
        iv,
        code
      },
      success: (res) => {
        if (res.data.success) {
          const phoneNumber = res.data.phoneNumber;
          // 更新用户信息中的手机号
          const userInfo = this.data.userInfo;
          userInfo.phoneNumber = phoneNumber;
          this.setData({
            userInfo: userInfo
          });
          wx.setStorageSync('userInfo', userInfo);
        }
      }
    });
    */
  },

  // 获取登录凭证
  getLoginCode() {
    return new Promise((resolve) => {
      wx.login({
        success: (res) => {
          resolve(res.code);
        }
      });
    });
  },

  goToMyActivities() {
    wx.navigateTo({
      url: '/pages/my_activities/index'
    });
  },

  goToSettings() {
    wx.navigateTo({
      url: '/pages/settings/index'
    });
  },

  // 切换标签
  switchTab: function (e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      currentTab: index
    });

    // 根据索引跳转到相应页面
    if (index === 0) {
      // 跳转到首页(tabBar页面)
      wx.reLaunch({
        url: '../index/index'
      });
    } else if (index === 2) {
      // 当前已在"我的"页面
      return;
    }
  }
});