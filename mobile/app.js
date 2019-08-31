//app.js
App({
  onLaunch: function () {
  },
  showError(msg){
    wx.showToast({
      title: msg,
      icon: '/images/close.png'
    })
  },
  globalData: {
    userInfo: null,
    host:'http://www.tunan.work:8080'
    // host:'http://192.168.43.27:8080'
    // host: 'http://192.168.41.26:8080'
  }
})