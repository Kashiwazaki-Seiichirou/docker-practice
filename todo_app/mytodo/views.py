from django.shortcuts import render, redirect
from django.views import View
from .models import Task
from.forms import TaskForm
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
class IndexView(View):
    def get(self, request):
        #todoリストを取得
        todo_list = Task.objects.all()
        
        context = {
            "todo_list": todo_list,
        }
        
        #テンプレートをレンダリング
        return render(request, "mytodo/index.html", context)
    
class AddView(View):
    def get(self, request):
        form = TaskForm()
        
        #テンプレートのレンダリング処理
        return render(request, "mytodo/add.html", {'form': form})
        
    def post(self, request, *args, **kwargs):
        #登録処理
        #入力データをフォームに渡す
        form = TaskForm(request.POST)
        #入力データに誤りがないかのチェック
        is_valid = form.is_valid()
        
        #データが正常であれば
        if is_valid:
            #モデルに登録
            form.save()
            return redirect('/')
        
        #データが正常じゃない場合
        return render(request, 'mytodo/add.html', {'form': form})
        
class Update_task_complete(View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        
        task = Task.objects.get(id=task_id)
        task.complete = not task.complete
        task.save()
        
        return redirect('/')
    
    
class HenshuView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        return render(request, "mytodo/henshu.html", {'form': form, 'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'mytodo/henshu.html', {'form': form, 'task': task})
      
      
class DeleteView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        return render(request, "mytodo/delete.html", {'form': form, 'task': task})
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return redirect('/')
      
#ビュークラスをインスタンス化
index = IndexView.as_view()
add = AddView.as_view()
update_task_complete = Update_task_complete.as_view()
henshu = HenshuView.as_view()
delete = DeleteView.as_view()

        