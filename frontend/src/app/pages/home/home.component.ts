import {Component, OnInit} from '@angular/core';
import {IrisService} from "./iris.service";
import {
    Iris,
    ProbabilityPrediction,
    SVCParameters,
    SVCResult
} from "./types";

@Component({
    selector: 'home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

    public svcParameters: SVCParameters = new SVCParameters();
    public svcResult: SVCResult;
    public iris: Iris = new Iris();
    public probabilityPredictions: ProbabilityPrediction[];
    public  result: String;
    // graph styling
    public colorScheme = {
        domain: ['#1a242c', '#e81746', '#e67303', '#f0f0f0']
    };

    constructor(private irisService: IrisService) {
    }

    ngOnInit() {
    }

    public predictIris() {
       console.log('Inside logs')
        this.irisService.predictIris(this.iris).subscribe((result) => {
            console.log(result._body)
            this.result = result._body;
        });
    }

}
