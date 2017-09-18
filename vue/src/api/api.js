const _fetch = fetch

export async function get (first, ...other) {
  let url = `${process.env.API_PREFIX}${first}`
  let res = await _fetch(url, ...other)
  return res
}

export async function post (first, data, ...other) {
  let url = `${process.env.API_PREFIX}${first}`
  let res = await _fetch(url, {
    method: 'POST',
    header: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  return res
}
