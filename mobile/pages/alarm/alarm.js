// pages/construction/message/message.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    active:'all'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this
    //获取接收警报列表
    wx.request({
      url: app.globalData.host + "/peoplecount/selectAlarm?offset=0&limit=5",
      dataType:'json',
      success(res){
        console.log(res.data)
        //抽取关键数据
        res.data = res.data.map((x)=>{
          x.fields.aid = x.pk
          x.fields.shottime = x.fields.atime.slice(14, 19)
          return x.fields
        })
        that.setData({alarmList:res.data})
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

  setRead:function(e){
    console.log(e)
    if(this.data.active == 'all' && !e.currentTarget.dataset.read)
    {
      this.setData({active:'unread'})
    } else if (this.data.active == 'unread' && e.currentTarget.dataset.read)
    {
      this.setData({active:'all'})
    }
  }
})