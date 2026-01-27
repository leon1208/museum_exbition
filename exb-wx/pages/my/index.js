// pages/my/index.js
Page({
  data: {
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
    console.log(wx.getAccountInfoSync())
    this.setData({
      version: version
    });
  },

  handleLogin() {
    // 处理用户登录
    const that = this;
    wx.getUserProfile({
      desc: '用于完善会员资料',
      success: (res) => {
        const userInfo = res.userInfo;
        wx.setStorageSync('userInfo', userInfo);
        this.setData({
          userInfo: userInfo
        });
      },
      fail: () => {
        wx.showToast({
          title: '登录失败',
          icon: 'none'
        });
      }
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