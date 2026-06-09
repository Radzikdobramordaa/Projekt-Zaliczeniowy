import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { CurrencyService } from './services/currency';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html'
  
})
export class AppComponent implements OnInit {

  years: number[] = [];
  months: number[] = [];
  quarters: number[] = [];

  selectedYear: string = '';
  selectedMonth: string = '';
  selectedQuarter: string = '';

  currencies: any[] = [];

  constructor(
    private currencyService: CurrencyService
  ) {}

  ngOnInit(): void {
    this.loadCurrencies();

    this.currencyService.getYears().subscribe(data => {this.years = data;});
    this.currencyService.getMonths().subscribe(data => {this.months = data;});
    this.currencyService.getQuarters().subscribe(data => {this.quarters = data;});

  }

  loadCurrencies(): void {
    this.currencyService
      .getCurrencies()
      .subscribe(data => {

        console.log('DANE Z API:', data);

        this.currencies = data;

        console.log(
          'LICZBA REKORDÓW:',
          this.currencies.length
        );

      });
  }

  fetchCurrencies(): void {
    this.currencyService
      .fetchCurrencies()
      .subscribe(() => {
        this.loadCurrencies();
      });
  }
  filteredCurrencies() {

    return this.currencies.filter(currency => {

      const date = new Date(
        currency.rate_date
      );

      const year =
        date.getFullYear();

      const month =
        date.getMonth() + 1;

      const quarter =
        Math.floor((month - 1) / 3) + 1;

      const yearMatch =
        !this.selectedYear ||
        year === Number(this.selectedYear);

      const monthMatch =
        !this.selectedMonth ||
        month === Number(this.selectedMonth);

      const quarterMatch =
        !this.selectedQuarter ||
        quarter === Number(this.selectedQuarter);

      return (
        yearMatch &&
        monthMatch &&
        quarterMatch
      );

    });

  }
}