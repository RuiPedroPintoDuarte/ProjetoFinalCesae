package pt.natixis.Backend_Java;

import pt.natixis.Backend_Java.model.Cliente;
import pt.natixis.Backend_Java.model.InfoBancaria;

import java.time.LocalDate;
import java.time.Period;
import java.util.Arrays;

public class MachineLearning {

    private static double[] coef = {-0.0119959, -0.00217458,  0.38130206,  1.18193011,  0.45408607,  0.72000208,
            0.25939667,  0.66366742,  0.09063038, -1.07007236,  0.19278002,  0.74977259,
            -0.68202608, -0.33307161, -0.1550227,  -0.03792849, -0.48789817,  0.13164846,
            -0.44537675,  0.745556};

    private static double intercept = -2.9089218279853046;

    private static double[] translateInfoBancariaToX(InfoBancaria info){
        Cliente cliente = info.getCliente();
        int age = Period.between(cliente.getDataNascimento(), LocalDate.now()).getYears();
        String job = info.getEmprego();
        String estadoCivil = info.getEstadoCivil();
        String educacao = info.getEducacao();

        double[] x = new double[20];
        x[0] = age;
        x[1] = info.getSaldo();

        if (job.equals("blue-collar")) { x[2] = 1;}
        else if (job.equals("entrepreneur")) {x[3] = 1;}
        else if (job.equals("housemaid")) { x[4] = 1; }
        else if (job.equals("management")) { x[5] = 1; }
        else if (job.equals("retired")) { x[6] = 1; }
        else if (job.equals("self-employed")) { x[7] = 1; }
        else if (job.equals("services")) { x[8] = 1; }
        else if (job.equals("student")) { x[9] = 1; }
        else if (job.equals("technician")) { x[10] = 1; }
        else if (job.equals("unemployed")) { x[11] = 1; }
        else { x[12] = 1; }

        if (estadoCivil.equals("married")){x[13] =1;}
        else if (estadoCivil.equals("single")){x[14] = 1;}

        if(educacao.equals("secondary")){x[15] =1;}
        else if(educacao.equals("tertiary")){x[16] =1;}
        else {x[17] =1;}

        if(info.getEmprestimoCasa()){x[18] =1;}
        if(info.getEmprestimoPessoal()){x[19] =1;}

        return x;
    }

    public static double predict(InfoBancaria info) {
        double[] x = translateInfoBancariaToX(info);
        double z = intercept;
        System.out.println(Arrays.toString(x));
        for (int i = 0; i < x.length; i++) {
            z += coef[i] * x[i];
        }
        double prob = 1.0 / (1.0 + Math.exp(-z));
        double percent = prob * 100;
        double roundedPercent = Math.round(percent * 100.0) / 100.0;

        return roundedPercent;
    }
}
