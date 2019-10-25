import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// import 'rxjs/add/operator/catch'

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    query = '';

    constructor(private http: HttpClient) {}
    arrayFaseDeGrupos: any;
    arrayPlayoffs: any;
    playoffsNaoClassificado: string;
    arrayFinalFaseDeGrupos: any;
    final: any;

    ngOnInit() {
        this.recuperaFinalFaseDeGrupos();
        this.recuperaFinal();
    }

    simular() {
        const auth = btoa("user:user-pass");
        const headers = {
            'Authorization': 'Basic ' + auth
        };

        this.http.get('https://ri-me.herokuapp.com/simular', {headers: headers})
        .subscribe(res => {},
            err => {
                this.arrayFaseDeGrupos = undefined;
                this.arrayPlayoffs = undefined;
                this.playoffsNaoClassificado = undefined;
                this.recuperaFinalFaseDeGrupos();
                this.recuperaFinal();
                alert(err.error.text);
            }
        );
    }

    recuperaFaseDeGrupos(time: string) {
        // encode base64
        const auth = btoa("user:user-pass");
        const headers = {
            'Authorization': 'Basic ' + auth
        };

        this.http.get('https://ri-me.herokuapp.com/time/fase-de-grupos/' + time, {headers: headers})
        .subscribe(res => {
            this.arrayFaseDeGrupos = res;
        });
    }

    recuperaPlayoffs(time: string) {
        // https://ri-me.herokuapp.com/time/partidas-playoffs/<numero-que-representa-o-time>
        const auth = btoa("user:user-pass");
        const headers = {
            'Authorization': 'Basic ' + auth
        };

        this.http.get('https://ri-me.herokuapp.com/time/partidas-playoffs/' + time, {headers: headers})
        .subscribe(
            res => {
                this.arrayPlayoffs = res;
            },
            err => {
                this.playoffsNaoClassificado = err.error.split('\n')[0];
        });
    }

    recuperaFinalFaseDeGrupos() {
        // arrayFinalFaseDeGrupos
        const auth = btoa("user:user-pass");
        const headers = {
            'Authorization': 'Basic ' + auth
        };

        this.http.get('https://ri-me.herokuapp.com/pontuacao-final-grupos', {headers: headers})
        .subscribe(res => {
            this.arrayFinalFaseDeGrupos = res;
        });
    }

    recuperaFinal() {
        // https://ri-me.herokuapp.com/final
        const auth = btoa("user:user-pass");
        const headers = {
            'Authorization': 'Basic ' + auth
        };

        this.http.get('https://ri-me.herokuapp.com/final', {headers: headers})
        .subscribe(res => {
            console.log(res);
            this.final = res;
        });
    }

    search() {
        if (Number(this.query)){
            const time = +this.query;

            if (time < 1 || time > 80) {
                alert('Digite um time que esteja entre 1 e 80.');
            }

            this.recuperaFaseDeGrupos(this.query);
            this.recuperaPlayoffs(this.query);
        } else {
            alert('Digite um time que seja um número e que esteja entre 1 e 80.');
        }
    }
}
