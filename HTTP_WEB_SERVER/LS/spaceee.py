range_request = "1-2,3-4,5-"
ranges = []
for r in range_request.replace('bytes=', '').split(','):
   start, end = r.split('-')
   start = int(start)
   end = int(end) if end else None
   ranges.append((start, end))
   print(ranges)
p = b'12345'
print(len(p))
print(p[0:4])

Response_header = {
  'Content-Type': 'text/html; charset=utf-8',
}
header = {
  'Content-Type': 'treertreretre',
}
for rq_key,rq_value in header.items():
  Response_header[rq_key] = rq_value
print(Response_header)