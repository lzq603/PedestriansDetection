// pages/alarmThreshold/alarmThreshold.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    sites:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this
    wx.request({
      url: app.globalData.host + '/getSites',
      success(res){
        console.log(res)
        let sites = res.data.map((x)=>{return x.fields})
        that.setData({sites:sites})
      },
      fail(res){
        console.log(res)
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  setAlarm: function(e){
    console.log(e)
    let site = e.currentTarget.dataset.site
    let alarm = e.detail.value
    wx.request({
      url: app.globalData.host + '/setAlarm?site=' + site + '&alarmThreshold=' + alarm,
      success(res){
        console.log(res)
        if(res.data.status = 'OK'){
          wx.showToast({
            title: '保存成功'
          })
        }else{
          app.showError('内部服务器错误')
        }
      },
      fail(res){
        app.showError('网络错误')
      }
    })
  }
})