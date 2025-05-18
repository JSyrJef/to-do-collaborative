import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { AuthCredentials, AuthResponse } from '../models/auth.model';
import { User } from '../models/user.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly TOKEN_KEY = 'auth_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private readonly USER_KEY = 'current_user';

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(
    this.hasToken()
  );
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(private http: HttpClient) {}

  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }
  register(user: User & AuthCredentials): Observable<User> {
    return this.http.post<User>(`${environment.apiUrl}/register/`, user);
  }

  login(credentials: AuthCredentials): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${environment.apiUrl}/login/`, credentials)
      .pipe(
        tap((response) => {
          localStorage.setItem(this.TOKEN_KEY, response.access);
          localStorage.setItem(this.REFRESH_TOKEN_KEY, response.refresh);
          localStorage.setItem(
            this.USER_KEY,
            JSON.stringify({ username: credentials.username })
          );
          this.isAuthenticatedSubject.next(true);
        })
      );
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.isAuthenticatedSubject.next(false);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  getCurrentUser(): User | null {
    const user = localStorage.getItem(this.USER_KEY);
    return user ? JSON.parse(user) : null;
  }

  private hasToken(): boolean {
    return !!this.getToken();
  }

  refreshToken(): Observable<{ access: string }> {
    return this.http
      .post<{ access: string }>(`${environment.apiUrl}/token/refresh/`, {
        refresh: this.getRefreshToken(),
      })
      .pipe(
        tap((response) => {
          localStorage.setItem(this.TOKEN_KEY, response.access);
          this.isAuthenticatedSubject.next(true);
        })
      );
  }
}
