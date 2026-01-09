import request from '@/utils/request'

// 查询博物馆媒体列表
export function listMuseumMedia(params) {
  return request({
    url: '/exb_museum/museum/media/list',
    method: 'get',
    params: params
  })
}

// 上传博物馆媒体
export function uploadMuseumMedia(data) {
  return request({
    url: '/exb_museum/museum/media/upload',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: data
  })
}

// 删除博物馆媒体
export function deleteMuseumMedia(mediaId) {
  return request({
    url: '/exb_museum/museum/media/' + mediaId,
    method: 'delete'
  })
}
