// 我的活动预约清单页面逻辑
import config from '../../../config/index.js';
import { api } from '../../../utils/api.js';

Page({
  /**
   * 页面的初始数据
   */
  data: {
    reservations: [],
    static_url: config.STATIC_URL
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.loadMyActivityReservations();
  },

  /**
   * 页面显示时重新加载数据
   */
  onShow: function () {
    // this.loadMyActivityReservations();
  },

  /**
   * 加载我的活动预约清单
   */
  loadMyActivityReservations: function () {
    wx.showLoading({
      title: '加载中...'
    });

    api.getMyActivityReservations()
      .then(response => {
        // console.log('获取我的活动预约成功', response);
        if (response.code === 200) {
          this.setData({
            reservations: response.data || []
          });
        } else {
          wx.showToast({
            title: response.msg || '获取预约信息失败',
            icon: 'error'
          });
        }
      })
      .catch(error => {
        // console.error('获取我的活动预约失败', error);
        wx.showToast({
          title: '获取预约信息失败',
          icon: 'error'
        });
      })
      .finally(() => {
        wx.hideLoading();
      });
  },

  /**
   * 取消预约活动
   */
  cancelReservation: function (event) {
    const reservationId = event.currentTarget.dataset.reservationId;
    const activityTitle = event.currentTarget.dataset.activityTitle;

    wx.showModal({
      title: '确认取消预约',
      content: `确定要取消预约"${activityTitle}"吗？`,
      success: (res) => {
        if (res.confirm) {
          api.cancelActivityReservation(reservationId)
            .then(response => {
              // console.log('取消预约成功', response);
              if (response.code === 200) {
                wx.showToast({
                  title: '取消预约成功',
                  icon: 'success'
                });             
                // 刷新页面   
                this.loadMyActivityReservations();
              } else {
                wx.showToast({
                  title: response.msg || '取消预约失败',
                  icon: 'error'
                });
              }
            })
            .catch(error => {
              wx.showToast({
                title: '取消预约失败',
                icon: 'error'
              });
            });
        } else if (res.cancel) {
          // console.log('用户取消取消预约');
        }
      }
    });
  },

  /**
   * 返回上一页
   */
  goBack: function () {
    wx.navigateBack();
  },
  
  /**
   * 跳转到活动页面
   */
  goToActivities: function () {
    wx.switchTab({
      url: '/pages/activities/index'
    });
  }
});
