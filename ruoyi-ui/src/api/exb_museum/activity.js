import request from '@/utils/request'

// 查询活动信息表列表
export function listActivity(query) {
  return request({
    url: '/exb_museum/activity/list',
    method: 'get',
    params: query
  })
}

// 查询活动信息表详细
export function getActivity(activityId) {
  return request({
    url: '/exb_museum/activity/' + activityId,
    method: 'get'
  })
}

// 新增活动信息表
export function addActivity(data) {
  return request({
    url: '/exb_museum/activity',
    method: 'post',
    data: data
  })
}

// 修改活动信息表
export function updateActivity(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/exb_museum/activity',
    method: 'put',
    data: data
  })
}

// 删除活动信息表
export function delActivity(activityId) {
  return request({
    url: '/exb_museum/activity/' + activityId,
    method: 'delete'
  })
}

// 批量删除活动信息表
export function batchDelActivity(activityIds) {
  return request({
    url: '/exb_museum/activity',
    method: 'delete',
    data: activityIds
  })
}

// 导出活动信息表
export function exportActivity(query) {
  return request({
    url: '/exb_museum/activity/export',
    method: 'get',
    params: query
  })
}

// 下载活动信息表导入模板
export function importTemplateActivity() {
  return request({
    url: '/exb_museum/activity/importTemplate',
    method: 'get'
  })
}

// 导入活动信息表
export function importActivity(data) {
  return request({
    url: '/exb_museum/activity/importData',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: data
  })
}