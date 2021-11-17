from django.shortcuts import render

# Create your views here.
def main(request):
    h_loss = [1,2,3,4,5]
    h_acc = [50, 60, 70, 80]
    h2_loss = [1,2,3,4,5]
    h2_acc = [50, 60, 70, 80]
    return render(request, 'main.html', {'h_loss':h_loss, 'h_acc':h_acc, 'h2_loss':h2_loss, 'h2_acc':h2_acc})
