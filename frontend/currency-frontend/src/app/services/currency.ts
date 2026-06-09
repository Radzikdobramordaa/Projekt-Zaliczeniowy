import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {

  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getCurrencies(): Observable<any> {
    return this.http.get(`${this.apiUrl}/currencies`);
  }

  fetchCurrencies(): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/currencies/fetch`,
      {}
    );
  }
  getYears(): Observable<any> {
    return this.http.get(`${this.apiUrl}/currencies/years`);
  }
  getMonths(): Observable<any> {
    return this.http.get(`${this.apiUrl}/currencies/months`);
  }
  getQuarters(): Observable<any> {
    return this.http.get(`${this.apiUrl}/currencies/quarters`);
  }
}