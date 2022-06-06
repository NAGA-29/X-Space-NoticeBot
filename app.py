from chalice import Chalice, Rate

app = Chalice(app_name='Twitter-Space-NoticeBot')

# Automatically runs every 5 minutes
@app.schedule(Rate(5, unit=Rate.MINUTES))
def Main(event):
    print(event.to_dict())