%%Man/Auto Analysis Code Update w GNL Removal%%
%%yes gabby this is the final final one you used lol%%

%fid = fopen('CF_Filenames.txt');
%tline  = fgetl(fid);
%while ischar(tline)
%list1 = fopen('AAM_1in2_Threshold_Filenames.txt','r');
%list2 = fopen('AAM_1in10k_Threshold_Filenames.txt','r');
%formatSpec = '%s';
%1in2list = fscanf(list1,formatSpec);
%1in10klist = fscanf(list2,formatSpec);
%fclose(list1);
%fclose(list2);

%1in2list = readlines('AAM_1in2_Threshold_Filenames.txt')
%1in10klist = readlines('AAM_1in10k_Threshold_Filenames.txt')

%fid = fopen('AAM_1in10k_Threshold_Filenames.txt');
fid = fopen('bookEx1.txt');
tline  = fgetl(fid);
while ischar(tline)
    tline = fgetl(fid);
    %f1 = fullfile('MORPHImages/AAM_1in10k_Threshold',[tline '.JPG']);
    %f2 = fullfile('MORPHImages/AAM_1in10k_BGRemoved',[tline '.png']);
    f1 = fullfile('bookEx1',[tline '.JPG']);
    f2 = fullfile('ExBGR',[tline '.png']);
    if (tline ~= -1)
        % Read images
        a = imread(f1); %Original image   
        b = imread(f2); %Image without background
        bgOnly = imsubtract(a,b); %Background only
        
        % Check for sufficient background
        % bgCheck = nnz(bgOnly);
        % TODO: if insufficient, skip image
        
        % Compute linear version of image
        gamma = 2.2;
        linR = double(a(:,:,1)).^gamma;
        linG = double(a(:,:,2)).^gamma;
        linB = double(a(:,:,3)).^gamma;
        
        % Compute linear version of background only
        gR = double(bgOnly(:,:,1)).^gamma;
        gG = double(bgOnly(:,:,2)).^gamma;
        gB = double(bgOnly(:,:,3)).^gamma;
        
        % Find non-zero pixels of linear background
        Rave1 = gR(gR~=0);
        Gave1 = gG(gG~=0);
        Bave1 = gB(gB~=0);
        
        % Compute mean of linear background pixels
        Rave = mean(Rave1);
        Gave = mean(Gave1);
        Bave = mean(Bave1);
        
        % Compute color correction factor from linear background image
        R_const = 0.18/Rave;
        G_const = 0.18/Gave;
        B_const = 0.18/Bave;
        
        % Correct the full linear image
        linR_corr = linR*R_const;
        linG_corr = linG*G_const;
        linB_corr = linB*B_const;
        
        % Add back nonlinearity
        finR = linR_corr.^(1/2.2);
        finG = linG_corr.^(1/2.2);
        finB = linB_corr.^(1/2.2);
        finImg = cat(3,finR,finG,finB);

        c = fullfile('ExFinal',[tline '.png']);
        imwrite(finImg, c);  
        fprintf("img done!")
    end
end
