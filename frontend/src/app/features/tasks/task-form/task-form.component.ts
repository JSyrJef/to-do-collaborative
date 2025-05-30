import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { TaskService } from '../../../core/services/task.service';
import { CommonModule, Location } from '@angular/common';

@Component({
  selector: 'app-task-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule, FormsModule],
  templateUrl: './task-form.component.html',
  styleUrl: './task-form.component.css'
})
export class TaskFormComponent implements OnInit {
  taskForm: FormGroup;
  loading = false;
  isEditMode = false;
  taskId: number | null = null;
  collaboratorUsername = '';
  error = '';
  addCollaboratorError = '';
  collaborators: string[] = [];
  
  constructor(
    private formBuilder: FormBuilder,
    private taskService: TaskService,
    private route: ActivatedRoute,
    private router: Router,
    private location: Location
  ) {
    this.taskForm = this.formBuilder.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      description: [''],
      status: ['pending', Validators.required],
      collaborators: [[]]
    });
  }
  
  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.isEditMode = true;
        this.taskId = +params['id'];
        this.loadTask();
      }
    });
  }
  
  loadTask(): void {
    if (!this.taskId) return;
    
    this.loading = true;
    this.taskService.getTask(this.taskId)
      .subscribe({
        next: task => {
          this.taskForm.patchValue({
            title: task.title,
            description: task.description,
            status: task.status
          });
          this.taskForm.patchValue({ collaborators: task.collaborators || [] });
          this.loading = false;
        },
        error: () => {
          this.loading = false;
          this.router.navigate(['/tasks']);
        }
      });
  }
  
  onSubmit(): void {
    if (this.taskForm.invalid) {
      return;
    }
    
    this.loading = true;
    this.error = '';
    
    if (this.isEditMode && this.taskId) {
      this.taskService.updateTask(this.taskId, this.taskForm.value)
        .subscribe({
          next: () => {
            this.router.navigate([`/tasks/${this.taskId}`]);
          },
          error: error => {
            this.error = error.error.detail || 'Ha ocurrido un error al actualizar la tarea';
            this.loading = false;
          }
        });
    } else {
      this.taskService.createTask(this.taskForm.value)
        .subscribe({
          next: () => {
            this.router.navigate(['/tasks']);
          },
          error: error => {
            this.error = error.error.detail || 'Ha ocurrido un error al crear la tarea';
            this.loading = false;
          }
        });
    }
  }
  
  addCollaborator(): void {
    if (!this.collaboratorUsername || !this.taskId) return;
    
    this.addCollaboratorError = '';
    this.taskService.addCollaborator(this.taskId, this.collaboratorUsername)
      .subscribe({
        next: () => {
          this.collaboratorUsername = '';
          this.loadTask(); // Recargar tarea para ver colaboradores actualizados
        },
        error: error => {
          this.addCollaboratorError = error.error.detail || 'Error al añadir colaborador';
        }
      });
  }
  
  removeCollaborator(username: string): void {
    if (!this.taskId) return;
    
    this.taskService.removeCollaborator(this.taskId, username)
      .subscribe({
        next: () => {
          const current = this.taskForm.value.collaborators || [];
          this.taskForm.patchValue({ collaborators: current.filter((collab: string) => collab !== username) });
        }
      });
  }

  goBack(): void {
    this.location.back();
  }
}