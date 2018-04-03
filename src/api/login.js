import request from '@/utils/request'

const base = '/api'

export function loginByUsername(username, password) {
  const data = {
    username,
    password
  }
  return request({
    url: `${base}/login`,
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: `${base}/logout`,
    method: 'post'
  })
}

export function getUserInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

