import {Injectable} from '@angular/core';
import {Http} from "@angular/http";
import {Observable} from "rxjs/Observable";
import 'rxjs/add/operator/map';
import {
    Iris,
    ProbabilityPrediction,
    SVCParameters,
    SVCResult
} from "./types";

const SERVER_URL: string = 'https://swiftml.vantage-env2.vantage-demo.demos.teradatacloud.io/iris/predict';

@Injectable()
export class IrisService {

    constructor(private http: Http) {
    }

    public predictIris(iris: Iris): Observable<any> {
        console.log('Print predictIris')
        return this.http.post(`${SERVER_URL}`, iris);
    }
}
