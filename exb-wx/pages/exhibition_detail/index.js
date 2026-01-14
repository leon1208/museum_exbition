Page({
  data: {
    showTitle: false
  },

  onScroll(e) {
    const show = e.detail.scrollTop > 200
    if (show !== this.data.showTitle) {
      this.setData({ showTitle: show })
    }
  },

  onBack() {
    wx.navigateBack()
  }
})
