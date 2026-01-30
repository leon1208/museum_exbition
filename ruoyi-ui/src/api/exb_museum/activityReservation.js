import request from '@/utils/request'

// 查询活动预约列表
export function listActivityReservation(activityId) {
  return request({
    url: '/exb_museum/activity/reservation/' + activityId,
    method: 'get'
  })
}

// 删除活动预约
export function delActivityReservation(reservationId) {
  return request({
    url: '/exb_museum/activity/reservation/' + reservationId,
    method: 'delete'
  })
}