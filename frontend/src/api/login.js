import request from '@/utils/request'

const base = '/api'

export function loginByUsername(username, password) {
  // const data = JSON.stringify({
  const data = {
    'username': username,
    'password': password
  }
  return request({
    url: `${base}/login`,
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'application/json'
    }
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

