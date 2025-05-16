export type TaskStatus = 
  | 'pending'
  | 'in_progress'
  | 'completed'
  | 'archived'
  | 'deleted'
  | 'canceled'
  | 'failed'
  | 'on_hold'
  | 'skipped'
  | 'paused'
  | 'resumed'
  | 'rejected'
  | 'approved';

export interface Task {
    id?: number;
    title: string;
    description: string;
    status: TaskStatus;
    created_at?: string;
    updated_at?: string;
    owner?: string;
    collaborators?: string[];
}

