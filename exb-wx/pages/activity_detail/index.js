// 教育活动详情页面逻辑
import config from '../../config/index.js';
import { api } from '../../utils/api.js';

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
      this.loadEducationDetail(education.id);
    }
  },

  loadEducationDetail: function (educationId) {
    api.getEducationDetail(educationId)
    .then(response => {
      const education = response.data;
      this.setData({
        education: education
      });
    })
    .catch(error => {
      console.error('获取活动详情失败', error);
      wx.showToast({
        title: '获取活动详情失败',
        icon: 'error'
      });
    });
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
          // console.log('用户确认报名', education.id);
          // 这里可以调用报名接口
          api.addActivityReservation(education.id, '')
          .then(response => {
            // console.log('报名成功', response);
            if (response.code === 200) {
              wx.showToast({
                title: '报名成功',
                icon: 'success'
              });
            }
            // 刷新活动详情
            this.loadEducationDetail(education.id);
          })
          .catch(error => {
            // console.error('报名失败', error);
            wx.showToast({
              title: '报名失败',
              icon: 'error'
            });
          });
        } else if (res.cancel) {
          // console.log('用户取消报名');
        }
      }
    });
  },
    // 取消报名活动
  cancelRegisterActivity: function () {
    const education = this.data.education;
    wx.showModal({
      title: '确认取消报名',
      content: `确定要取消报名参加"${education.title}"吗？`,
      success: (res) => {
        if (res.confirm) {
          // console.log('用户确认取消报名', education.id);
          // 这里可以调用取消报名接口
          api.cancelActivityReservation(education.reservationId)
          .then(response => {
            // console.log('取消报名成功', response);
            if (response.code === 200) {
              wx.showToast({
                title: '取消报名成功',
                icon: 'success'
              });
            }
            // 刷新活动详情
            this.loadEducationDetail(education.id);
          })
          .catch(error => {
            // console.error('取消报名失败', error);
            wx.showToast({
              title: '取消报名失败',
              icon: 'error'
            });
          });
        } else if (res.cancel) {
          // console.log('用户取消取消报名');
        }
      }
    });
  },
  
});
