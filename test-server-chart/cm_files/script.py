try:
    import tensorflow as tf
    import torch
    import json
    from functools import wraps
    import numpy as np
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, Input
except Exception as ex:
    print(f'Image missing a necessary package: {ex}')
    quit()
def log_errors(f):
    @wraps(f)
    def inner_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            args[0]['msg'] = str(ex)
    return inner_function

@log_errors
def is_tensorflow_available(log):
    try:
        # check GPUs
        gpus = tf.config.list_physical_devices('GPU')
        log['tensorflow'] = len(gpus) > 0
        if log['tensorflow']:
            log['msg'] += 'succesfully detected GPUs using tensorflow'

        # Run ML model
        X = np.random.random((100, 16))
        y = np.random.randint(0, 2, size=(100,))
        tf.config.set_visible_devices(gpus[0], 'GPU')
        inputs = Input(shape=X.shape[1:])
        x = Dense(4, activation="tanh")(inputs)
        outputs = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer="sgd", loss="binary_crossentropy")
        model.fit(X, y, verbose=1, epochs=1, batch_size=1)

        log['tensorflow'] = True
        log['msg'] += 'succesfully ran basic ML model using GPUs with tensorflow'

    except Exception as e:
        print(e)
        log['tensorflow'] = False
        log['msg'] += 'tensorflow error = {e}'


@log_errors
def is_torch_available(log):
    log['torch'] = torch.cuda.is_available()


if __name__ == '__main__':
    log = {'torch':False, 'tensorflow': False, 'msg':'' }
    is_tensorflow_available(log)
    is_torch_available(log)
    print(json.dumps(log,indent=2))