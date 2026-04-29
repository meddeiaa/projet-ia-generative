import { Injectable, isDevMode } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

// ======================================================
// INTERFACES
// ======================================================

export interface GenerateRequest {
  prompt: string;
}

export interface ImageRequest {
  prompt: string;
  style?: string;
}

export interface GenerateResponse {
  success: boolean;
  result: string;
}

export interface HistoryItem {
  id: number;
  generation_type: 'text' | 'image' | 'video';  // ← précis
  prompt: string;
  style?: string;
  result?: string;
  created_at: string;
}

export interface HistoryResponse {
  items: HistoryItem[];
  total: number;
}

// ======================================================
// SERVICE
// ======================================================

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = isDevMode()
    ? 'http://localhost:8000'
    : 'https://projet-ia-generative.onrender.com';

  constructor(private http: HttpClient) {
    console.log(`🌐 API URL: ${this.baseUrl}`);
  }

  // ======================================================
  // GÉNÉRATION
  // ======================================================

  generateText(prompt: string): Observable<GenerateResponse> {
    return this.http.post<GenerateResponse>(
      `${this.baseUrl}/generate/text`,
      { prompt }
    ).pipe(catchError(this.handleError));
  }

  generateImage(prompt: string, style: string = 'general'): Observable<GenerateResponse> {
    return this.http.post<GenerateResponse>(
      `${this.baseUrl}/generate/image`,
      { prompt, style }
    ).pipe(catchError(this.handleError));
  }

  generateVideo(prompt: string): Observable<Blob> {
    return this.http.post(
      `${this.baseUrl}/generate/video`,
      { prompt },
      { responseType: 'blob' }
    ).pipe(catchError(this.handleError));
  }

  // ======================================================
  // HISTORIQUE
  // ======================================================

  getHistory(): Observable<HistoryResponse> {
    return this.http.get<HistoryResponse>(
      `${this.baseUrl}/history`
    ).pipe(catchError(this.handleError));
  }

  deleteHistory(id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/history/${id}`
    ).pipe(catchError(this.handleError));
  }

  // ======================================================
  // GESTION DES ERREURS
  // ======================================================

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Une erreur est survenue';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Erreur: ${error.error.message}`;
    } else {
      errorMessage = `Erreur ${error.status}: ${error.message}`;
    }

    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}