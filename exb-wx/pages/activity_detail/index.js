// 教育活动详情页面逻辑
import config from '../../config/index.js';

Page({
  /**
   * 页面的初始数据
   */
  data: {
    education: {},
    static_url: config.STATIC_URL
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 从页面参数获取教育活动数据
    if (options.activity) {
      const education = JSON.parse(options.activity);
      this.setData({
        education: education
      });
    }
  },

  /**
   * 返回上一页
   */
  goBack: function () {
    wx.navigateBack();
  },

  /**
   * 报名活动
   */
  registerActivity: function () {
    const education = this.data.education;
    wx.showModal({
      title: '确认报名',
      content: `确定要报名参加"${education.title}"吗？`,
      success: (res) => {
        if (res.confirm) {
          console.log('用户确认报名', education.id);
          // 这里可以调用报名接口
          wx.showToast({
            title: '报名成功',
            icon: 'success'
          });
        } else if (res.cancel) {
          console.log('用户取消报名');
        }
      }
    });
  }
});
