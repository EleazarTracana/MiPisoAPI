from fastapi import FastAPI

app = FastAPI();

test_array = [1,2,3,4,5]

@app.get('/api/v1/health')
async def get_health_status():
    prints = forEach(10)
    for item in test_array:
        prints += str(item)
    return {"Message": prints}

def forEach(myrange: int):
    final_prints = "Print "
    for i in range(myrange):
        final_prints += str(i)
    return final_prints





