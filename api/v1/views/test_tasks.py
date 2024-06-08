from api.v1.views import app_views
from flask import jsonify


@app_views.route('/test_tasks', methods=['GET'], strict_slashes=False)
def test_tasks():
    """Test tasks"""
    from api.v1.helpers.tasks.celery_tasks import test_task
    test_task.delay()
    return jsonify({"message": "Task started"}), 200