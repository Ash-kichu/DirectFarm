from django.shortcuts import render

# Create your views here.
def home(request):
    reviews = [
        {
            "content": "DirectFarm has completely changed the way we buy produce. We love knowing exactly where our food is coming from, and everything we’ve ordered has been incredibly fresh. It feels great to support local farmers!", "author": "Customer"
        },
        {
            "content": "As someone who values sustainable food, DirectFarm is perfect. The produce is always top-quality, and I love that it’s farm-to-table. I’m never going back to the grocery store for vegetables!", "author": "Customer"
        },
        {
            "content": "The variety and quality of produce from DirectFarm is amazing! I can taste the difference, and I feel like I’m doing my part to support our local farmers. It’s fresh, fair, and reliable.", "author": "Customer"
        },
        # {
        #     "content": "DirectFarm has completely changed the way we buy produce. We love knowing exactly where our food is coming from, and everything we’ve ordered has been incredibly fresh. It feels great to support local farmers!", "author": "Customer"
        # },
        # {
        #     "content": "As someone who values sustainable food, DirectFarm is perfect. The produce is always top-quality, and I love that it’s farm-to-table. I’m never going back to the grocery store for vegetables!", "author": "Customer"
        # },
        # {
        #     "content": "The variety and quality of produce from DirectFarm is amazing! I can taste the difference, and I feel like I’m doing my part to support our local farmers. It’s fresh, fair, and reliable.", "author": "Customer"
        # },
    ]
    context = {'reviews': reviews}

    return render(request, 'home.html', context)
