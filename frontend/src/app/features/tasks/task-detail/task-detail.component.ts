import { Component, OnInit } from '@angular/core';
import { TaskService } from '../../../core/services/task.service';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { Task } from '../../../core/models/task.model';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-task-detail',
  standalone: true,
  imports: [CommonModule, RouterModule,MatIconModule],
  templateUrl: './task-detail.component.html',
  styleUrl: './task-detail.component.css'
})
export class TaskDetailComponent implements OnInit {
  task!: Task;
  loading = false;

  constructor(private taskService: TaskService, private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id')); // obtiene el id de la ruta
    this.loading = true;
    this.taskService.getTask(id).subscribe({
      next: (t) => {
        this.task = t;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al obtener tarea:', err);
        this.loading = false;
      }
    });
  }

  completeTask(): void {
    this.taskService.updateTask(this.task.id!, { status: 'completed' })
      .subscribe({
        next: (updatedTask) => this.task = updatedTask
      });
  }

  reopenTask(): void {
    this.taskService.updateTask(this.task.id!, { status: 'pending' })
      .subscribe({
        next: (updatedTask) => this.task = updatedTask
      });
  }

  deleteTask(): void {
    if (confirm('Estas seguro de que quieres eliminar esta tarea?')) {
      this.taskService.deleteTask(this.task.id!)
        .subscribe({
          next: () => {
            console.log('Tarea eliminada');
            this.router.navigate(['/tasks']);
          }
        });
    }
  }
}
