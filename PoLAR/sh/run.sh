
export root_dir="<your-path>/worksapce/PoLAR/PoLAR"
dataset_dir=<your-path>/datasets/retriever

#? cuda:x
device=cuda:2

#? train test analyze
do=train

#! backdoor
#? nq hotpotqa trivia
dataset_names=(nq)
#? badnets addsent hidden-killer stylebkd
attack_methods=(badnets)
poison_rates=(0.1)
#? BERT BGE UAE
pretrain_models=(UAE)
sactter_per_samples=1000

#! train
train_mode=loss
batch_size=64
train_capacity=-1
test_capacity=1000

#! defense
#? none badacts musclelora onion strip cube bki polar
defense_methods=(polar)

# ours_lowup_detecter
lowup_sample_capacity=32
lowup_train_batch_size=16

#! analyze
# analyze_sample_tot=5000
analyze_sample_tot=1000

#! search
#? all
sampling_methods=(all)
#? dot cosine
distance_metrics=(dot)
#? triplet contrastive infoNCE CE
loss_functions=(CE)
margins=(0.1)

for dataset_name in "${dataset_names[@]}"; do
for attack_method in "${attack_methods[@]}"; do
for sampling_method in "${sampling_methods[@]}"; do
for distance_metric in "${distance_metrics[@]}"; do
for loss_function in "${loss_functions[@]}"; do
for poison_rate in "${poison_rates[@]}"; do
for defense_method in "${defense_methods[@]}"; do
for pretrain_model in "${pretrain_models[@]}"; do

if [[ "$sampling_method" == "random" || "$sampling_method" == "hard" ]] &&
    [[ "$loss_function" == "infoNCE" || "$loss_function" == "CE" ]]; then
    continue
elif [[ "$sampling_method" == "all" ]] &&
    [[ "$loss_function" == "triplet" || "$loss_function" == "contrastive" ]]; then
    continue
fi

if [ "$dataset_name" = "nq" ]; then
    epochs=5
elif [ "$dataset_name" = "hotpotqa" ]; then
    epochs=3
elif [ "$dataset_name" = "trivia" ]; then
    epochs=3
fi

if [ "$train_mode" = "grad" ]; then
    epochs=1
fi

if [ "$pretrain_model" = "BGE" ]; then
    batch_size=32
    if [ "$defense_method" = "ours_lowup_detecter" ]; then
        batch_size=24
        lowup_sample_capacity=16
        lowup_train_batch_size=8
    fi
elif [ "$pretrain_model" = "UAE" ]; then
    batch_size=32
    if [ "$defense_method" = "ours_lowup_detecter" ]; then
        batch_size=32
        lowup_sample_capacity=16
        lowup_train_batch_size=8
    fi
fi

# echo "[shell] epochs: $epochs"

clean_train_dataset=${dataset_name}_train
clean_test_dataset=${dataset_name}_dev
poisoned_train_dataset=${dataset_name}_poisoned_train_${attack_method}_${poison_rate}
poisoned_test_dataset=${dataset_name}_poisoned_test_${attack_method}_${poison_rate}

output_dir=YourPath/${pretrain_model}/${dataset_name}/${attack_method}/${poison_rate}/${sampling_method}/${distance_metric}/${loss_function}/capacity-${train_capacity}/epochs-${epochs}/train-mode-${train_mode}/defense-${defense_method}

mkdir -p ${output_dir}

cd ${root_dir}

if [ "$do" = "train" ]; then

python ${root_dir}/train_dense_encoder.py \
    action=train \
    train_datasets=[${clean_train_dataset},${poisoned_train_dataset}] \
    test_datasets=[${clean_test_dataset},${poisoned_test_dataset}] \
    train=biencoder_local \
    defense=${defense_method} \
    epochs=${epochs} \
    batch_size=${batch_size} \
    train_capacity=${train_capacity} \
    test_capacity=${test_capacity} \
    sampling_method=${sampling_method} \
    distance_metric=${distance_metric} \
    loss_function=${loss_function} \
    train_mode=${train_mode} \
    output_dir=${output_dir} \
    sactter_per_samples=${sactter_per_samples} \
    device=${device} \
    dataset_name=${dataset_name} \
    dataset_dir=${dataset_dir} \
    attack_method=${attack_method} \
    lowup_sample_capacity=${lowup_sample_capacity} \
    lowup_train_batch_size=${lowup_train_batch_size} \
    poison_rate=${poison_rate} \
    encoder=${pretrain_model}
wait

elif [ "$do" = "test" ]; then

python train_dense_encoder.py \
    action=test \
    train_datasets=[${clean_train_dataset},${poisoned_train_dataset}] \
    test_datasets=[${clean_test_dataset},${poisoned_test_dataset}] \
    train=biencoder_local \
    defense=${defense_method} \
    epochs=${epochs} \
    batch_size=${batch_size} \
    train_capacity=${train_capacity} \
    test_capacity=${test_capacity} \
    sampling_method=${sampling_method} \
    distance_metric=${distance_metric} \
    loss_function=${loss_function} \
    train_mode=${train_mode} \
    output_dir=${output_dir} \
    sactter_per_samples=${sactter_per_samples} \
    device=${device} \
    dataset_name=${dataset_name} \
    dataset_dir=${dataset_dir} \
    attack_method=${attack_method} \
    poison_rate=${poison_rate}
wait

elif [ "$do" == "analyze" ]; then

analyze_title=$attack_method-$poison_rate

python train_dense_encoder.py \
    action=analyze \
    train_datasets=[${clean_train_dataset},${poisoned_train_dataset}] \
    test_datasets=[${clean_test_dataset},${poisoned_test_dataset}] \
    train=biencoder_local \
    defense=${defense_method} \
    epochs=${epochs} \
    batch_size=${batch_size} \
    train_capacity=${train_capacity} \
    test_capacity=${test_capacity} \
    sampling_method=${sampling_method} \
    distance_metric=${distance_metric} \
    loss_function=${loss_function} \
    train_mode=${train_mode} \
    output_dir=${output_dir} \
    sactter_per_samples=${sactter_per_samples} \
    device=${device} \
    dataset_name=${dataset_name} \
    analyze_sample_tot=${analyze_sample_tot} \
    analyze_title=${analyze_title} \
    dataset_dir=${dataset_dir} \
    attack_method=${attack_method} \
    poison_rate=${poison_rate}
wait

fi

done
done
done
done
done
done
done
done