const _fetch = fetch

export async function get (first, ...other) {
  let url = `${process.env.API_PREFIX}${first}`
  let res = await _fetch(url, ...other)
  return res
}

